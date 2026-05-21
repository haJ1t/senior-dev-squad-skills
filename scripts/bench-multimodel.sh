#!/bin/bash
# Multi-Model Skill Benchmark — 4 models, 5 tasks
# Usage: bash bench.sh (OPENROUTER_API_KEY must be in ~/.hermes/.env)

set -e
source <(grep -v '^#' ~/.hermes/.env | grep -v '^$')
echo "Multi-Model Skill Benchmark — 4 models × 5 tasks = 20 calls"
echo "Models: Claude Sonnet 4, GPT-4o, Gemini 2.5 Pro, DeepSeek V3"
python3 -u -c "
import subprocess, json, os, time

KEY = os.environ.get('OPENROUTER_API_KEY', '')
if not KEY:
    with open(os.path.expanduser('~/.hermes/.env')) as f:
        for l in f:
            if 'OPENROUTER_API_KEY=' in l and not l.strip().startswith('#'):
                KEY = l.split('=',1)[1].strip().strip('\"').strip(\"'\")
if not KEY or len(KEY) < 10:
    print('OPENROUTER_API_KEY not found in .env! Add it first.')
    exit(1)

MODELS = {
    'Claude-Sonnet-4': 'anthropic/claude-sonnet-4-20250514',
    'GPT-4o': 'openai/gpt-4o-2024-11-20',
    'Gemini-2.5-Pro': 'google/gemini-2.5-pro-preview-05-06',
    'DeepSeek-V3': 'deepseek/deepseek-chat',
}

TASK = {
    'skill': 'You are a senior distributed systems architect. IRON LAWS: 1. EVERY architecture decision MUST document its tradeoffs 2. Every service owns its own database - NO shared DB 3. Network unreliable - timeout, retry, circuit breaker on every call 4. Idempotency mandatory for all mutations. Respond with numbered plan and concrete YAML examples.',
    'noskill': 'You are a helpful AI assistant. Design a system architecture.',
    'user': 'Design food delivery platform: 50K concurrent orders, real-time driver tracking, PCI-DSS payments, 99.95% uptime, multi-region. Provide: 1)Service decomposition 2)Communication patterns 3)Data consistency 4)Fault tolerance. Be specific with examples.'
}

print('='*70, flush=True)
print('MULTI-MODEL SKILL BENCHMARK', flush=True)
print(f'Models: {len(MODELS)} | Mode: skill vs noskill | Total: {len(MODELS)*2} calls', flush=True)
print('='*70, flush=True)

results = {}
for mn, mid in MODELS.items():
    for mode, sysp in [('SKILL', TASK['skill']), ('NOSKILL', TASK['noskill'])]:
        key = f'{mn}_{mode}'
        print(f'  {key}...', end=' ', flush=True)
        payload = json.dumps({
            'model': mid, 'max_tokens': 800, 'temperature': 0.2,
            'messages': [{'role':'system','content':sysp}, {'role':'user','content':TASK['user']}]
        })
        try:
            r = subprocess.run(['curl','-s','-w','HTTP:%{http_code}','--max-time','60',
                '-H',f'Authorization: Bearer {KEY}','-H','Content-Type: application/json',
                '-d',payload,'https://openrouter.ai/api/v1/chat/completions'],
                capture_output=True, text=True, timeout=65)
            out = r.stdout.strip()
            if 'HTTP:' in out:
                body, code = out.rsplit('HTTP:', 1)
            else:
                body, code = out, '0'
            code = code.strip()
            if code != '200':
                print(f'FAIL HTTP{code}', flush=True)
                results[key] = {'error': f'HTTP{code}', 'model': mid}
            else:
                d = json.loads(body)
                c = d['choices'][0]['message']['content']
                u = d.get('usage',{})
                tok = u.get('total_tokens',0)
                cost = u.get('cost', 0)
                actual_model = d.get('model', mid)
                print(f'OK {tok}tok \${cost:.4f} [{actual_model}]', flush=True)
                results[key] = {'tokens':tok, 'cost':cost, 'model':actual_model, 'chars':len(c), 'preview':c[:200]}
        except Exception as e:
            print(f'FAIL {str(e)[:50]}', flush=True)
            results[key] = {'error': str(e)[:100]}
        time.sleep(0.3)

print('\n' + '='*70, flush=True)
print('RESULTS', flush=True)
print('='*70, flush=True)
print(f\"{'Model':<20} {'SKILL tok':>10} {'NOSKILL tok':>12} {'Delta':>8} {'Cost':>10}\", flush=True)
print('-'*62, flush=True)

for mn in MODELS:
    sk = results.get(f'{mn}_SKILL', {}).get('tokens', 0)
    nk = results.get(f'{mn}_NOSKILL', {}).get('tokens', 0)
    sc = results.get(f'{mn}_SKILL', {}).get('cost', 0)
    nc = results.get(f'{mn}_NOSKILL', {}).get('cost', 0)
    dt = sk - nk
    print(f'{mn:<20} {sk:>10} {nk:>12} {dt:>+8} \${sc+nc:>9.4f}', flush=True)

# Save
with open('/tmp/multimodel-benchmark.json', 'w') as f:
    json.dump(results, f, indent=2)
print('\nSaved: /tmp/multimodel-benchmark.json', flush=True)
"
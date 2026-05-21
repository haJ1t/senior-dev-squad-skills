---
name: mobile-pro
description: "React Native / Flutter / SwiftUI: state management, navigation, offline, push, stores. Use when building or reviewing mobile apps."
---

# Mobile Pro

## Purpose

Build production-grade mobile apps. Covers React Native, Flutter, and SwiftUI patterns: state management, navigation, offline-first, push notifications, app store deployment.

## When to Use

**Use this when:**
- Building or extending a React Native, Flutter, or SwiftUI application targeting iOS or Android
- Architecting offline-first behavior, background sync, or push notification flows
- Preparing an app for App Store or Google Play submission and need to pass platform review requirements

**Use this ESPECIALLY when:**
- The app must function with intermittent connectivity (field workers, travel, low-signal regions)
- Implementing deep linking, universal links, or notification-driven navigation where native integration is required
- Optimizing a FlatList, image pipeline, or JS thread workload after profiling shows frame drops on mid-range devices

**Don't skip when:**
- Adding any permission request (camera, location, health, contacts) — purpose strings and just-in-time prompts are required by both stores
- Introducing a new native module that requires bridging between JS and platform code
- Releasing a major version update where state shape or navigation structure has changed and migration from installed versions is needed

## Core Patterns (React Native)

### 1. Project Structure

```
src/
  components/        ← Reusable UI components
  screens/           ← Screen-level components
  navigation/        ← React Navigation config
  services/          ← API, push, analytics
  store/             ← State management (zustand/redux)
  hooks/             ← Custom hooks
  utils/             ← Formatters, validators
  constants/         ← Colors, typography, config
  types/             ← TypeScript types
  native/            ← Native modules (iOS/Android)
__tests__/
```

### 2. State Management

```typescript
// Zustand (lightweight)
import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'
import AsyncStorage from '@react-native-async-storage/async-storage'

interface ProjectStore {
  projects: Project[]
  isLoading: boolean
  error: string | null
  fetchProjects: () => Promise<void>
  createProject: (name: string) => Promise<void>
}

export const useProjectStore = create<ProjectStore>()(
  persist(
    (set, get) => ({
      projects: [],
      isLoading: false,
      error: null,

      fetchProjects: async () => {
        set({ isLoading: true, error: null })
        try {
          const projects = await api.getProjects()
          set({ projects, isLoading: false })
        } catch (err) {
          set({ error: err.message, isLoading: false })
        }
      },

      createProject: async (name) => {
        const project = await api.createProject(name)
        set({ projects: [project, ...get().projects] })
      },
    }),
    {
      name: 'project-storage',
      storage: createJSONStorage(() => AsyncStorage),
      partialize: (state) => ({ projects: state.projects }),
    }
  )
)
```

### 3. Offline-First

```typescript
// Network-aware data fetching
import NetInfo from '@react-native-community/netinfo'

async function fetchWithOffline<T>(key: string, fetcher: () => Promise<T>): Promise<T> {
  const state = await NetInfo.fetch()

  if (!state.isConnected) {
    const cached = await AsyncStorage.getItem(key)
    if (cached) return JSON.parse(cached)
    throw new Error('No internet connection and no cached data')
  }

  try {
    const data = await fetcher()
    await AsyncStorage.setItem(key, JSON.stringify(data))
    return data
  } catch (err) {
    const cached = await AsyncStorage.getItem(key)
    if (cached) return JSON.parse(cached)
    throw err
  }
}
```

### 4. Push Notifications

```typescript
// OneSignal / Firebase Cloud Messaging
import { requestNotificationPermission } from './permissions'

async function setupPushNotifications() {
  const permission = await requestNotificationPermission()
  if (!permission) return

  // Register for push
  const token = await messaging().getToken()
  await api.registerPushToken(token)

  // Handle foreground messages
  messaging().onMessage(async (remoteMessage) => {
    showInAppNotification(remoteMessage)
  })

  // Handle background tap
  messaging().onNotificationOpenedApp((remoteMessage) => {
    navigateToScreen(remoteMessage.data.screen, remoteMessage.data.params)
  })
}
```

### 5. Performance

```typescript
// ✅ Image optimization
<FastImage
  source={{ uri: imageUrl, priority: FastImage.priority.high }}
  style={{ width: 200, height: 200 }}
  resizeMode={FastImage.resizeMode.contain}
/>

// ✅ FlatList optimization (not ScrollView for lists)
<FlatList
  data={projects}
  renderItem={renderProject}
  keyExtractor={(item) => item.id}
  initialNumToRender={10}
  maxToRenderPerBatch={10}
  windowSize={5}
  removeClippedSubviews={true}
  getItemLayout={getItemLayout}  // Fixed height = better perf
  ListEmptyComponent={<EmptyState />}
  ListFooterComponent={<LoadingSpinner />}
  onEndReached={loadMore}
  onEndReachedThreshold={0.5}
/>
```

## Flutter Specifics

```dart
// ✅ Riverpod for state management
final projectProvider = AsyncNotifierProvider<ProjectList, List<Project>>(
  ProjectList.new,
);

class ProjectList extends AsyncNotifier<List<Project>> {
  @override
  Future<List<Project>> build() async {
    return ref.read(projectRepositoryProvider).fetchAll();
  }

  Future<void> create(String name) async {
    final project = await ref.read(projectRepositoryProvider).create(name);
    state = AsyncData([project, ...state.value ?? []]);
  }
}
```

## App Store Checklist

- [ ] Offline state handled (no blank screens without network)
- [ ] Deep linking configured
- [ ] Push notifications working (foreground + background)
- [ ] App icons + splash screen configured
- [ ] Minimum deployed OS versions set
- [ ] Permission prompts have purpose strings (why camera, why location)
- [ ] Analytics integrated (Firebase / Mixpanel)
- [ ] Crash reporting (Sentry / Crashlytics)
- [ ] App size optimized (asset compression, code splitting)
- [ ] Accessibility: screen reader support, minimum touch targets
- [ ] iPad/Mac Catalyst layout tested (if universal)

## Related Skills

- **frontend-senior-engineer** — when shared business logic or component libraries span a web app and the React Native mobile app in the same repo
- **backend-senior-engineer** — for the API layer that the mobile app consumes, especially REST design, pagination, and push token registration endpoints
- **performance-engineer** — when JS thread, native bridge, or render pipeline profiling reveals bottlenecks beyond standard FlatList and image optimizations
- **accessibility-optimizer** — for VoiceOver/TalkBack compliance, minimum touch target enforcement, and dynamic type support
- **security-reviewer** — when the app stores tokens in AsyncStorage/Keychain, handles biometric auth, or sends sensitive data over the network
- **devops-release-engineer** — for Fastlane pipelines, code signing automation, TestFlight/Play Internal Track distribution, and over-the-air update strategies

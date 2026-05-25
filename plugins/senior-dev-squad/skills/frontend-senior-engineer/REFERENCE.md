# Frontend Senior Engineer — Worked Example

Companion to [SKILL.md](./SKILL.md). Full annotated code for the **Users List** feature:
RSC page shell → client list with all four states → create-user form with blur/submit
validation and double-submit prevention.

---

## Feature: Users List page

### 1. Page shell — React Server Component

```tsx
// app/users/page.tsx
// NO "use client" — this is an RSC.
// It can be async, can await server data, ships zero JS to the browser.

import { Suspense } from "react"
import { UsersList } from "./_components/UsersList"
import { CreateUserForm } from "./_components/CreateUserForm"
import { UsersListSkeleton } from "./_components/UsersListSkeleton"

export default function UsersPage() {
  // RSC choice: no useState, no useEffect, no browser APIs needed.
  // The interactive parts (list with refetch, form) are client components — see below.
  return (
    <main className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">Users</h1>

      {/* Suspense boundary → shows skeleton while UsersList's query resolves */}
      <Suspense fallback={<UsersListSkeleton />}>
        <UsersList />
      </Suspense>

      <section aria-labelledby="create-user-heading" className="mt-10">
        <h2 id="create-user-heading" className="text-xl font-semibold mb-4">
          Add a User
        </h2>
        <CreateUserForm />
      </section>
    </main>
  )
}
```

**Why RSC for the shell?** No interactivity at this level. RSC = zero client JS for the
wrapper, full SEO-friendly HTML, and `<Suspense>` streaming out of the box.

---

### 2. UsersList — client component, all four states

```tsx
// app/users/_components/UsersList.tsx
"use client"

import { useQuery } from "@tanstack/react-query"
import { UserCard } from "./UserCard"
import { ErrorState } from "@/components/ui/ErrorState"
import { EmptyState } from "@/components/ui/EmptyState"
import { Button } from "@/components/ui/Button"
import { fetchUsers, type User } from "@/lib/api/users"

export function UsersList() {
  const { data: users, isLoading, error, refetch } = useQuery<User[]>({
    queryKey: ["users"],
    queryFn: fetchUsers,
    // staleTime: 30_000 — omitted here for brevity; set per product requirement
  })

  // STATE 1: LOADING — show immediately, no artificial delay
  // Skeleton lives in the RSC's <Suspense> for first load;
  // this branch covers background re-fetches after the list is already mounted.
  if (isLoading) return <UsersListSkeleton />

  // STATE 2: ERROR — human-readable message + retry action
  if (error) return (
    <ErrorState
      title="Could not load users"
      message={error instanceof Error ? error.message : "An unexpected error occurred."}
      action={
        <Button onClick={() => refetch()} variant="secondary">
          Try again
        </Button>
      }
    />
  )

  // STATE 3: EMPTY — tell the user what to do next
  if (!users?.length) return (
    <EmptyState
      title="No users yet"
      description="Add your first user using the form below."
    />
  )

  // STATE 4: SUCCESS — render the list
  // Key choice: user.id (stable server ID), NOT array index.
  // Index keys break React's reconciler when items are deleted or reordered.
  return (
    <ul
      className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3"
      aria-label="Users list"
    >
      {users.map((user) => (
        <li key={user.id}>
          <UserCard user={user} />
        </li>
      ))}
    </ul>
  )
}
```

**Why React Query, not `useEffect`?** `useQuery` gives loading / error / stale states,
automatic deduplication, background refetch, and cache invalidation for free. A raw
`useEffect` with `useState` requires 40+ lines to replicate the same guarantees — and
most teams get the race condition or cleanup wrong.

---

### 3. CreateUserForm — blur + submit validation, double-submit prevention

```tsx
// app/users/_components/CreateUserForm.tsx
"use client"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { createUser } from "@/lib/api/users"
import { Button } from "@/components/ui/Button"
import { FieldError } from "@/components/ui/FieldError"

// 1. Schema first — single source of truth for validation rules
const schema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  email: z.string().email("Enter a valid email address"),
})
type FormValues = z.infer<typeof schema>

export function CreateUserForm() {
  const queryClient = useQueryClient()

  // 2. react-hook-form handles: blur validation, submit validation,
  //    field registration, error state, and isSubmitting guard.
  //    No manual useState needed for any of this.
  const {
    register,
    handleSubmit,
    setError,          // map server errors back to fields
    reset,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({
    resolver: zodResolver(schema),
    mode: "onBlur",   // validate on blur, not every keystroke
  })

  // 3. Mutation — invalidates the users cache on success so the list refetches
  const mutation = useMutation({
    mutationFn: createUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["users"] })
      reset()
    },
    onError: (err: unknown) => {
      // 4. Map server validation errors to specific fields when the API tells us
      if (isApiValidationError(err)) {
        err.fields.forEach(({ field, message }) => {
          setError(field as keyof FormValues, { message })
        })
      }
    },
  })

  // 5. onSubmit — double-submit is impossible: isSubmitting is true while the
  //    Promise is pending, and the button is disabled (see below).
  const onSubmit = (values: FormValues) => mutation.mutateAsync(values)

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      noValidate               // let our schema own validation, not the browser's native UI
      className="space-y-4 max-w-md"
      aria-label="Create user form"
    >
      <div>
        <label htmlFor="name" className="block text-sm font-medium mb-1">
          Full name <span aria-hidden="true">*</span>
        </label>
        <input
          id="name"
          type="text"
          autoComplete="name"
          aria-required="true"
          aria-describedby={errors.name ? "name-error" : undefined}
          aria-invalid={!!errors.name}
          className="w-full rounded border px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          {...register("name")}
        />
        {/* Inline error — NOT a toast, NOT an alert */}
        {errors.name && (
          <FieldError id="name-error" message={errors.name.message!} />
        )}
      </div>

      <div>
        <label htmlFor="email" className="block text-sm font-medium mb-1">
          Email address <span aria-hidden="true">*</span>
        </label>
        <input
          id="email"
          type="email"
          autoComplete="email"
          aria-required="true"
          aria-describedby={errors.email ? "email-error" : undefined}
          aria-invalid={!!errors.email}
          className="w-full rounded border px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          {...register("email")}
        />
        {errors.email && (
          <FieldError id="email-error" message={errors.email.message!} />
        )}
      </div>

      {/* General server error (non-field) */}
      {mutation.isError && !isApiValidationError(mutation.error) && (
        <p role="alert" className="text-sm text-red-600">
          Something went wrong. Please try again.
        </p>
      )}

      {/* 6. Double-submit prevention: disabled + aria-disabled during submission.
              aria-busy signals screen readers that something is happening. */}
      <Button
        type="submit"
        disabled={isSubmitting}
        aria-disabled={isSubmitting}
        aria-busy={isSubmitting}
      >
        {isSubmitting ? "Creating…" : "Create user"}
      </Button>
    </form>
  )
}

// Type guard — replace with your API error shape
function isApiValidationError(
  err: unknown
): err is { fields: Array<{ field: string; message: string }> } {
  return (
    typeof err === "object" &&
    err !== null &&
    "fields" in err &&
    Array.isArray((err as any).fields)
  )
}
```

---

### Decision narration — key choices made above

| Choice | Reason |
|--------|--------|
| RSC page shell, `"use client"` only on interactive parts | Zero client JS for the wrapper; Suspense streaming; SEO |
| `useQuery` not `useEffect + fetch` | Race-condition free; loading/error/stale for free; cache shared across routes |
| `key={user.id}` not `key={index}` | Index keys break diffing on delete/reorder; stable IDs are O(1) reconciliation |
| `mode: "onBlur"` in useForm | Validates after the user leaves the field, not on every keystroke (noisy) |
| `isSubmitting` from `useForm` disables button | No extra `useState`; automatically resets on settle; zero race condition |
| `setError` for server field errors | Maps API errors back to the correct field; user sees the error inline, not in a toast |
| `aria-invalid`, `aria-describedby`, `aria-busy` | Screen readers announce the error linked to the field and the submission state |
| `role="alert"` on general error | Live region — announced immediately without focus move |

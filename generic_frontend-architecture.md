# Frontend Architecture — Industry Reference Guide

---

## 1. Generic Component Taxonomy

### Layout Components
- **Shell / AppShell** — outermost wrapper; handles sidebars, topbars, footers
- **Grid / Container** — responsive column systems (12-col, CSS Grid, Flexbox wrappers)
- **Stack / Row / Column** — directional flex primitives
- **Divider / Spacer** — explicit whitespace control
- **Portal** — renders children outside the DOM tree (modals, tooltips)

### Navigation Components
- **Navbar / Topbar** — primary horizontal navigation
- **Sidebar / Drawer** — vertical collapsible navigation
- **Breadcrumb** — hierarchical path indicator
- **Tabs** — horizontal/vertical content switcher
- **Pagination** — page-based list navigation
- **Stepper** — multi-step wizard indicator

### Input / Form Components
- **Input** (text, number, password, search)
- **Textarea** — multi-line text
- **Select / Combobox / Autocomplete** — option picker
- **Checkbox / Radio / Switch** — boolean or grouped choice
- **DatePicker / TimePicker / DateRangePicker**
- **FileUpload / DropZone**
- **Slider / RangeSlider**
- **ColorPicker**
- **Form** — wrapper managing validation, submission, and error state
- **FormField / FormLabel / FormError** — field-level primitives

### Display / Feedback Components
- **Button / IconButton / ButtonGroup**
- **Badge / Tag / Chip** — status indicators
- **Avatar / AvatarGroup**
- **Card / Paper** — surface containers
- **Table / DataGrid** — tabular data (with sort, filter, pagination)
- **List / ListItem**
- **Tree / TreeNode** — nested hierarchy display
- **Timeline**
- **Stat / KPI Card** — metric highlight

### Overlay / Feedback Components
- **Modal / Dialog**
- **Drawer / Sheet** — sliding panel overlay
- **Popover / Dropdown**
- **Tooltip**
- **Toast / Snackbar / Notification** — ephemeral feedback
- **Alert / Banner** — persistent inline status messages
- **Spinner / Skeleton / ProgressBar** — loading states
- **ConfirmDialog** — destructive action gate

### Media Components
- **Image** (with lazy-load, aspect ratio, fallback)
- **Video / AudioPlayer**
- **Carousel / Swiper**
- **Map**
- **Chart / Graph** (line, bar, pie, area, scatter)
- **Icon** — SVG sprite wrapper

### Utility Components
- **ErrorBoundary** — React/Vue error containment
- **Suspense / LazyLoader** — async chunk loading
- **IntersectionObserver wrapper** — scroll-triggered logic
- **VirtualList / VirtualGrid** — windowed rendering for large lists
- **ResizeObserver wrapper**
- **Theme / ColorScheme provider**
- **I18n / Translation provider**

---

## 2. Industry-Standard Directory Structure

```
my-app/
├── public/                         # Static assets served as-is
│   ├── favicon.ico
│   ├── robots.txt
│   └── assets/
│       └── images/
│
├── src/
│   ├── app/                        # App bootstrap, routing root
│   │   ├── App.tsx
│   │   ├── router.tsx              # Route definitions (React Router / TanStack Router)
│   │   └── providers.tsx           # Global context/provider composition
│   │
│   ├── pages/                      # Route-level view components (thin)
│   │   ├── Home/
│   │   │   ├── index.tsx
│   │   │   └── Home.test.tsx
│   │   ├── Dashboard/
│   │   └── NotFound/
│   │
│   ├── features/                   # Domain-scoped vertical slices
│   │   ├── auth/
│   │   │   ├── components/
│   │   │   ├── hooks/
│   │   │   ├── store/              # Zustand slice or Redux slice
│   │   │   ├── api.ts              # Auth-specific API calls
│   │   │   └── types.ts
│   │   ├── users/
│   │   └── products/
│   │
│   ├── components/                 # Shared, reusable UI components
│   │   ├── ui/                     # Primitive / design-system components
│   │   │   ├── Button/
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Button.stories.tsx
│   │   │   │   ├── Button.test.tsx
│   │   │   │   └── index.ts
│   │   │   ├── Input/
│   │   │   ├── Modal/
│   │   │   └── ...
│   │   └── layout/                 # Layout wrappers
│   │       ├── Navbar/
│   │       ├── Sidebar/
│   │       └── PageWrapper/
│   │
│   ├── hooks/                      # Shared custom hooks
│   │   ├── useDebounce.ts
│   │   ├── useLocalStorage.ts
│   │   ├── useMediaQuery.ts
│   │   └── useIntersectionObserver.ts
│   │
│   ├── store/                      # Global state (Zustand / Redux)
│   │   ├── index.ts
│   │   ├── uiSlice.ts
│   │   └── authSlice.ts
│   │
│   ├── services/                   # API client & service modules
│   │   ├── api/
│   │   │   ├── client.ts           # Axios / fetch base instance
│   │   │   ├── interceptors.ts
│   │   │   └── endpoints.ts
│   │   └── analytics.ts
│   │
│   ├── lib/                        # Third-party wrappers & initializers
│   │   ├── queryClient.ts          # TanStack Query config
│   │   ├── i18n.ts
│   │   └── sentry.ts
│   │
│   ├── utils/                      # Pure utility functions
│   │   ├── formatters.ts
│   │   ├── validators.ts
│   │   └── constants.ts
│   │
│   ├── types/                      # Global TypeScript types & interfaces
│   │   ├── api.ts                  # API response shapes
│   │   ├── models.ts               # Domain models
│   │   └── globals.d.ts
│   │
│   ├── styles/                     # Global CSS / Tailwind base
│   │   ├── globals.css
│   │   ├── tokens.css              # CSS custom properties (design tokens)
│   │   └── animations.css
│   │
│   └── assets/                     # Imported assets (images, fonts, SVGs)
│       ├── fonts/
│       └── icons/
│
├── tests/
│   ├── e2e/                        # Playwright / Cypress
│   └── setup.ts                   # Vitest / Jest global setup
│
├── .env                            # Local env vars (never commit)
├── .env.example
├── index.html                      # Vite entry point
├── package.json
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.ts
└── vitest.config.ts
```

---

## 3. Key Files, Modules & Packages

### Core Framework

| Package                    | Role                    |
| -------------------------- | ----------------------- |
| `react` / `vue` / `svelte` | UI rendering            |
| `typescript`               | Static typing           |
| `vite`                     | Build tool & dev server |


### Routing

| Package                | Role                          |
| ---------------------- | ----------------------------- |
| `react-router-dom` v6+ | Client-side routing           |
| `@tanstack/router`     | Type-safe routing alternative |


### State Management

| Package                 | Role                        |
| ----------------------- | --------------------------- |
| `zustand`               | Lightweight global state    |
| `@reduxjs/toolkit`      | Structured global state     |
| `@tanstack/react-query` | Server state, caching, sync |
| `jotai` / `recoil`      | Atomic state                |


### Data Fetching

| Package                                      | Role                              |
| -------------------------------------------- | --------------------------------- |
| `axios`                                      | HTTP client with interceptors     |
| `ky`                                         | Fetch-based lightweight HTTP      |
| `@tanstack/react-query`                      | Declarative async data management |
| `swr`                                        | Stale-while-revalidate hook       |
| `graphql-request` / `urql` / `apollo-client` | GraphQL                           |


### Forms & Validation

| Package           | Role                                    |
| ----------------- | --------------------------------------- |
| `react-hook-form` | Performant uncontrolled forms           |
| `zod`             | Schema validation (shared with backend) |
| `yup`             | Schema validation alternative           |


### Styling

| Package             | Role                                  |
| ------------------- | ------------------------------------- |
| `tailwindcss`       | Utility-first CSS                     |
| `@emotion/react`    | CSS-in-JS                             |
| `styled-components` | CSS-in-JS alternative                 |
| `shadcn/ui`         | Radix-based headless component system |
| `radix-ui`          | Accessible headless primitives        |


### Animation

| Package          | Role                                |
| ---------------- | ----------------------------------- |
| `framer-motion`  | Declarative React animations        |
| `@motionone/dom` | Low-level web animations            |
| `gsap`           | Complex timelines & scroll triggers |


### Testing

| Package                  | Role                         |
| ------------------------ | ---------------------------- |
| `vitest`                 | Unit & integration testing   |
| `@testing-library/react` | Component testing            |
| `msw`                    | API mocking (service worker) |
| `playwright` / `cypress` | End-to-end testing           |
| `storybook`              | Component isolation & docs   |


### Tooling

| Package                 | Role                       |
| ----------------------- | -------------------------- |
| `eslint` + plugins      | Linting                    |
| `prettier`              | Code formatting            |
| `husky` + `lint-staged` | Pre-commit hooks           |
| `@commitlint/cli`       | Commit message enforcement |

---

## 4. How Modules Interact

```
┌─────────────────────────────────────────────────────────┐
│                        Browser                          │
│                                                         │
│  ┌──────────┐    ┌───────────────────────────────────┐  │
│  │  Router  │───▶│         Pages (route views)       │  │
│  └──────────┘    └──────────────┬────────────────────┘  │
│                                 │ renders               │
│                  ┌──────────────▼────────────────────┐  │
│                  │   Feature Modules (vertical slices)│  │
│                  │  ┌──────────┐  ┌────────────────┐  │  │
│                  │  │Components│  │  Custom Hooks   │ │  │
│                  │  └────┬─────┘  └───────┬────────┘  │  │
│                  └───────┼───────────────┼────────────┘  │
│                          │               │               │
│            ┌─────────────▼──┐    ┌───────▼───────────┐   │
│            │  Global Store  │    │   React Query /   │   │
│            │ (Zustand/Redux)│    │   Server State    │   │
│            └────────────────┘    └───────┬───────────┘   │
│                                          │               │
│                          ┌───────────────▼─────────┐     │
│                          │     API Service Layer    │    │
│                          │  (Axios instance +       │    │
│                          │   interceptors)          │    │
│                          └───────────────┬──────────┘    │
└──────────────────────────────────────────┼───────────────┘
                                           │ HTTP / WS
                                  ┌────────▼────────┐
                                  │   Backend API   │
                                  └─────────────────┘
```

**Data Flow Summary:**
1. **Router** matches URL → mounts **Page** component
2. **Page** composes **Feature** components
3. **Feature** components call **custom hooks** for logic
4. **Custom hooks** use **React Query** for server data OR **Zustand** for client-only state
5. **React Query** calls the **API Service Layer** (Axios instance)
6. **API Service Layer** attaches tokens (from store), sends request to backend
7. Response is cached by React Query; components re-render reactively

---

## 5. Do's / Don'ts / Best Practices

###  Do's

**Architecture**
- Use the **feature-based (vertical slice)** folder structure — keeps related code co-located
- Keep **pages thin** — they should compose features, not contain logic
- Separate **server state** (React Query) from **client/UI state** (Zustand)
- Use **TypeScript strictly** — enable `strict: true` in `tsconfig.json`
- Define **shared Zod schemas** that are importable on both FE and BE for end-to-end type safety
- Use **barrel files** (`index.ts`) to keep imports clean

**Components**
- Build components as **controlled** by default; lift state only when needed
- Apply the **compound component pattern** for complex, composable components
- Always handle **loading**, **error**, and **empty** states in data-fetching components
- Use **Radix UI / Headless UI** primitives for accessible overlays, not rolling your own

**Performance**
- Lazy-load routes with `React.lazy` + `Suspense`
- Virtualize long lists with `@tanstack/react-virtual`
- Memoize expensive derived data with `useMemo`; avoid premature `memo()` on every component
- Optimize images with `width`/`height` attributes and `loading="lazy"`

**Testing**
- Write tests that resemble how users interact (Testing Library philosophy)
- Mock the network at the MSW layer, not at the module level
- Test **behaviours**, not implementation details

**Security**
- Never store JWT tokens in `localStorage` — use `httpOnly` cookies
- Sanitize all HTML rendered via `dangerouslySetInnerHTML`
- Validate all form inputs on both client AND server side

###  Don'ts

- **Don't** mix server state and UI state in the same store slice
- **Don't** call APIs inside `useEffect` directly — use React Query
- **Don't** use `any` in TypeScript — use `unknown` and narrow the type
- **Don't** import from sibling feature modules — features must stay decoupled (use events or shared services)
- **Don't** keep secrets or API keys in frontend env vars prefixed with `VITE_` — they are bundled into the client
- **Don't** use array index as `key` prop in dynamic lists — use stable IDs
- **Don't** put business logic inside components — extract to hooks or services
- **Don't** nest context providers without measuring the re-render impact
- **Don't** disable ESLint rules inline without a comment explaining why

###  Design System Best Practices
- Define **design tokens** (colors, spacing, typography, shadows) as CSS variables early
- Build **primitive → composite → page** component hierarchy
- Version your component library with **changesets** if shared across projects
- Document all components with **Storybook** stories including all variants and edge-case states

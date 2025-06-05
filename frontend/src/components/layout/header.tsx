import { component$, type QRL } from '@builder.io/qwik';

interface HeaderProps {
  onToggleSidebar$: QRL<() => void>;
}

export const Header = component$<HeaderProps>(({ onToggleSidebar$ }) => {
  return (
    <header class="bg-white shadow-sm border-b border-gray-200">
      <div class="flex items-center justify-between px-6 py-4">
        {/* Left side */}
        <div class="flex items-center">
          <button
            onClick$={onToggleSidebar$}
            class="p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500"
            aria-label="Toggle sidebar"
          >
            <svg
              class="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
          </button>
        </div>

        {/* Center - Search */}
        <div class="flex-1 max-w-lg mx-8">
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg
                class="h-5 w-5 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                />
              </svg>
            </div>
            <input
              type="text"
              placeholder="Search schedules, routes, employees..."
              class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary-500 focus:border-primary-500"
            />
          </div>
        </div>

        {/* Right side */}
        <div class="flex items-center space-x-4">
          {/* Notifications */}
          <button class="p-2 text-gray-400 hover:text-gray-500 relative">
            <svg
              class="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M15 17h5l-5 5v-5zM10.5 3.5a6 6 0 0 1 6 6v2l1.5 3h-15l1.5-3v-2a6 6 0 0 1 6-6z"
              />
            </svg>
            <span class="absolute top-0 right-0 block h-2 w-2 rounded-full bg-error-400 ring-2 ring-white"></span>
          </button>

          {/* Real-time status */}
          <div class="flex items-center space-x-2">
            <div class="w-2 h-2 bg-success-400 rounded-full animate-pulse"></div>
            <span class="text-sm text-gray-600">Live</span>
          </div>

          {/* Current time */}
          <div class="text-sm text-gray-600">
            {new Date().toLocaleTimeString()}
          </div>
        </div>
      </div>
    </header>
  );
});
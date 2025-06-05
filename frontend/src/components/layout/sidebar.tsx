import { component$, type Signal } from '@builder.io/qwik';
import { Link, useLocation } from '@builder.io/qwik-city';

interface SidebarProps {
  isOpen: Signal<boolean>;
}

export const Sidebar = component$<SidebarProps>(({ isOpen }) => {
  const location = useLocation();

  const navigation = [
    {
      name: 'Dashboard',
      href: '/',
      icon: '📊',
      current: location.url.pathname === '/',
    },
    {
      name: 'Organizations',
      href: '/organizations',
      icon: '🏢',
      current: location.url.pathname.startsWith('/organizations'),
    },
    {
      name: 'Employees',
      href: '/employees',
      icon: '👥',
      current: location.url.pathname.startsWith('/employees'),
    },
    {
      name: 'Schedules',
      href: '/schedules',
      icon: '📅',
      current: location.url.pathname.startsWith('/schedules'),
    },
    {
      name: 'Timesheets',
      href: '/timesheets',
      icon: '⏰',
      current: location.url.pathname.startsWith('/timesheets'),
    },
    {
      name: 'Routes',
      href: '/routes',
      icon: '🗺️',
      current: location.url.pathname.startsWith('/routes'),
    },
    {
      name: 'Vehicles',
      href: '/vehicles',
      icon: '🚛',
      current: location.url.pathname.startsWith('/vehicles'),
    },
    {
      name: 'Forecasting',
      href: '/forecasting',
      icon: '📈',
      current: location.url.pathname.startsWith('/forecasting'),
    },
    {
      name: 'Reports',
      href: '/reports',
      icon: '📋',
      current: location.url.pathname.startsWith('/reports'),
    },
  ];

  return (
    <div
      class={`fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out ${
        isOpen.value ? 'translate-x-0' : '-translate-x-full'
      }`}
    >
      {/* Logo */}
      <div class="flex items-center justify-center h-16 px-4 bg-primary-600">
        <h1 class="text-xl font-bold text-white">
          WMS Intelligence
        </h1>
      </div>

      {/* Navigation */}
      <nav class="mt-8 px-4">
        <ul class="space-y-2">
          {navigation.map((item) => (
            <li key={item.name}>
              <Link
                href={item.href}
                class={`group flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors ${
                  item.current
                    ? 'bg-primary-100 text-primary-700 border-r-2 border-primary-500'
                    : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                }`}
              >
                <span class="mr-3 text-lg">{item.icon}</span>
                {item.name}
              </Link>
            </li>
          ))}
        </ul>
      </nav>

      {/* User Section */}
      <div class="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-200">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-primary-500 rounded-full flex items-center justify-center">
              <span class="text-white text-sm font-medium">JD</span>
            </div>
          </div>
          <div class="ml-3">
            <p class="text-sm font-medium text-gray-700">John Doe</p>
            <p class="text-xs text-gray-500">Administrator</p>
          </div>
        </div>
      </div>
    </div>
  );
});
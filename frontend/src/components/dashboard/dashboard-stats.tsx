import { component$ } from '@builder.io/qwik';

export const DashboardStats = component$(() => {
  const stats = [
    {
      name: 'Active Routes Today',
      value: '127',
      change: '+12%',
      changeType: 'positive',
      icon: '🗺️',
    },
    {
      name: 'Crews On Duty',
      value: '89',
      change: '+5%',
      changeType: 'positive',
      icon: '👥',
    },
    {
      name: 'Vehicles Active',
      value: '64',
      change: '-2%',
      changeType: 'negative',
      icon: '🚛',
    },
    {
      name: 'Completion Rate',
      value: '94.2%',
      change: '+1.8%',
      changeType: 'positive',
      icon: '✅',
    },
  ];

  return (
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {stats.map((stat) => (
        <div key={stat.name} class="card">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
                <span class="text-2xl">{stat.icon}</span>
              </div>
            </div>
            <div class="ml-4 flex-1">
              <p class="text-sm font-medium text-gray-600">{stat.name}</p>
              <div class="flex items-baseline">
                <p class="text-2xl font-semibold text-gray-900">{stat.value}</p>
                <p
                  class={`ml-2 text-sm font-medium ${
                    stat.changeType === 'positive'
                      ? 'text-success-600'
                      : 'text-error-600'
                  }`}
                >
                  {stat.change}
                </p>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
});
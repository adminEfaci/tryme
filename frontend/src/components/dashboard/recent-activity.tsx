import { component$ } from '@builder.io/qwik';

export const RecentActivity = component$(() => {
  const activities = [
    {
      id: '1',
      type: 'schedule_completed',
      message: 'Route A completed by Team Alpha',
      timestamp: '2 minutes ago',
      icon: '✅',
      iconColor: 'text-success-500',
    },
    {
      id: '2',
      type: 'timesheet_submitted',
      message: 'John Smith submitted timesheet for Week 23',
      timestamp: '15 minutes ago',
      icon: '⏰',
      iconColor: 'text-primary-500',
    },
    {
      id: '3',
      type: 'vehicle_maintenance',
      message: 'Vehicle WM-005 scheduled for maintenance',
      timestamp: '32 minutes ago',
      icon: '🔧',
      iconColor: 'text-warning-500',
    },
    {
      id: '4',
      type: 'new_assignment',
      message: 'Emergency cleanup assigned to Team Charlie',
      timestamp: '1 hour ago',
      icon: '🚨',
      iconColor: 'text-error-500',
    },
    {
      id: '5',
      type: 'forecast_generated',
      message: 'Weekly capacity forecast generated',
      timestamp: '2 hours ago',
      icon: '📈',
      iconColor: 'text-primary-500',
    },
    {
      id: '6',
      type: 'contractor_approved',
      message: 'Green Valley Waste Services approved',
      timestamp: '3 hours ago',
      icon: '🏢',
      iconColor: 'text-success-500',
    },
  ];

  return (
    <div class="card">
      <div class="flex items-center justify-between mb-6">
        <h3 class="text-lg font-medium text-gray-900">Recent Activity</h3>
        <button class="btn-outline text-sm">View All</button>
      </div>

      <div class="flow-root">
        <ul class="-mb-8">
          {activities.map((activity, index) => (
            <li key={activity.id}>
              <div class="relative pb-8">
                {index !== activities.length - 1 && (
                  <span
                    class="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200"
                    aria-hidden="true"
                  />
                )}
                <div class="relative flex space-x-3">
                  <div>
                    <span
                      class={`h-8 w-8 rounded-full bg-gray-100 flex items-center justify-center ring-8 ring-white ${activity.iconColor}`}
                    >
                      <span class="text-sm">{activity.icon}</span>
                    </span>
                  </div>
                  <div class="flex-1 min-w-0">
                    <div>
                      <p class="text-sm text-gray-900">{activity.message}</p>
                      <p class="text-xs text-gray-500">{activity.timestamp}</p>
                    </div>
                  </div>
                </div>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
});
import { component$ } from '@builder.io/qwik';

export const ScheduleOverview = component$(() => {
  const schedules = [
    {
      id: '1',
      route: 'Downtown Core - Route A',
      crew: 'Team Alpha',
      vehicle: 'WM-001',
      status: 'in_progress',
      progress: 65,
      estimatedCompletion: '14:30',
    },
    {
      id: '2',
      route: 'Residential West - Route B',
      crew: 'Team Beta',
      vehicle: 'WM-002',
      status: 'completed',
      progress: 100,
      estimatedCompletion: '13:45',
    },
    {
      id: '3',
      route: 'Industrial Zone - Route C',
      crew: 'Team Gamma',
      vehicle: 'WM-003',
      status: 'scheduled',
      progress: 0,
      estimatedCompletion: '16:00',
    },
    {
      id: '4',
      route: 'Suburban East - Route D',
      crew: 'Team Delta',
      vehicle: 'WM-004',
      status: 'in_progress',
      progress: 35,
      estimatedCompletion: '15:15',
    },
  ];

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'completed':
        return 'badge-success';
      case 'in_progress':
        return 'badge-primary';
      case 'scheduled':
        return 'badge-secondary';
      default:
        return 'badge-secondary';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'completed':
        return 'Completed';
      case 'in_progress':
        return 'In Progress';
      case 'scheduled':
        return 'Scheduled';
      default:
        return 'Unknown';
    }
  };

  return (
    <div class="card">
      <div class="flex items-center justify-between mb-6">
        <h3 class="text-lg font-medium text-gray-900">Today's Schedule Overview</h3>
        <button class="btn-outline text-sm">View All</button>
      </div>

      <div class="space-y-4">
        {schedules.map((schedule) => (
          <div key={schedule.id} class="border border-gray-200 rounded-lg p-4">
            <div class="flex items-center justify-between mb-3">
              <div class="flex-1">
                <h4 class="text-sm font-medium text-gray-900">{schedule.route}</h4>
                <p class="text-sm text-gray-600">
                  {schedule.crew} • {schedule.vehicle}
                </p>
              </div>
              <div class="flex items-center space-x-3">
                <span class={`badge ${getStatusBadge(schedule.status)}`}>
                  {getStatusText(schedule.status)}
                </span>
                <span class="text-sm text-gray-500">
                  ETA: {schedule.estimatedCompletion}
                </span>
              </div>
            </div>

            {/* Progress Bar */}
            <div class="w-full bg-gray-200 rounded-full h-2">
              <div
                class={`h-2 rounded-full transition-all duration-300 ${
                  schedule.status === 'completed'
                    ? 'bg-success-500'
                    : schedule.status === 'in_progress'
                    ? 'bg-primary-500'
                    : 'bg-gray-300'
                }`}
                style={`width: ${schedule.progress}%`}
              ></div>
            </div>
            <div class="flex justify-between text-xs text-gray-500 mt-1">
              <span>Progress</span>
              <span>{schedule.progress}%</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
});
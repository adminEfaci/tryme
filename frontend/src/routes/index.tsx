import { component$ } from '@builder.io/qwik';
import type { DocumentHead } from '@builder.io/qwik-city';
import { DashboardStats } from '~/components/dashboard/dashboard-stats';
import { RecentActivity } from '~/components/dashboard/recent-activity';
import { ScheduleOverview } from '~/components/dashboard/schedule-overview';

export default component$(() => {
  return (
    <div class="space-y-6">
      {/* Page Header */}
      <div class="border-b border-gray-200 pb-4">
        <h1 class="text-2xl font-bold text-gray-900">
          Waste Management Dashboard
        </h1>
        <p class="mt-1 text-sm text-gray-600">
          Overview of operations, schedules, and performance metrics
        </p>
      </div>

      {/* Dashboard Stats */}
      <DashboardStats />

      {/* Main Content Grid */}
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Schedule Overview */}
        <div class="lg:col-span-1">
          <ScheduleOverview />
        </div>

        {/* Recent Activity */}
        <div class="lg:col-span-1">
          <RecentActivity />
        </div>
      </div>
    </div>
  );
});

export const head: DocumentHead = {
  title: 'Dashboard - Waste Management Intelligence System',
  meta: [
    {
      name: 'description',
      content: 'Municipal-grade waste logistics platform dashboard with real-time operations overview',
    },
  ],
};
import { component$, useSignal, useTask$ } from '@builder.io/qwik';
import type { DocumentHead } from '@builder.io/qwik-city';
import { OrganizationList } from '~/components/organizations/organization-list';
import { OrganizationForm } from '~/components/organizations/organization-form';

export default component$(() => {
  const showCreateForm = useSignal(false);
  const organizations = useSignal<any[]>([]);
  const loading = useSignal(true);

  // Simulate API call - in real app this would use TanStack Query
  useTask$(async () => {
    try {
      // Mock data for demonstration
      await new Promise(resolve => setTimeout(resolve, 1000));
      organizations.value = [
        {
          id: '1',
          name: 'City Waste Management',
          organization_type: 'prime_contractor',
          status: 'active',
          primary_contact_name: 'John Smith',
          primary_contact_email: 'john@citywaste.com',
          primary_contact_phone: '+1-613-555-0123',
          city: 'Ottawa',
          province_state: 'Ontario',
          max_capacity_hours_per_day: 480,
          performance_score: 95.5,
        },
        {
          id: '2',
          name: 'Green Valley Services',
          organization_type: 'subcontractor',
          status: 'active',
          primary_contact_name: 'Sarah Johnson',
          primary_contact_email: 'sarah@greenvalley.com',
          primary_contact_phone: '+1-613-555-0456',
          city: 'Kanata',
          province_state: 'Ontario',
          max_capacity_hours_per_day: 320,
          performance_score: 88.2,
        },
      ];
      loading.value = false;
    } catch (error) {
      console.error('Failed to load organizations:', error);
      loading.value = false;
    }
  });

  return (
    <div class="space-y-6">
      {/* Page Header */}
      <div class="flex items-center justify-between border-b border-gray-200 pb-4">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Organizations</h1>
          <p class="mt-1 text-sm text-gray-600">
            Manage contractors, subcontractors, and municipal organizations
          </p>
        </div>
        <button
          onClick$={() => showCreateForm.value = true}
          class="btn-primary"
        >
          <span class="mr-2">+</span>
          Add Organization
        </button>
      </div>

      {/* Stats Cards */}
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div class="card">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-primary-100 rounded-lg flex items-center justify-center">
                <span class="text-primary-600">🏢</span>
              </div>
            </div>
            <div class="ml-3">
              <p class="text-sm font-medium text-gray-600">Total Organizations</p>
              <p class="text-lg font-semibold text-gray-900">{organizations.value.length}</p>
            </div>
          </div>
        </div>
        
        <div class="card">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-success-100 rounded-lg flex items-center justify-center">
                <span class="text-success-600">✅</span>
              </div>
            </div>
            <div class="ml-3">
              <p class="text-sm font-medium text-gray-600">Active</p>
              <p class="text-lg font-semibold text-gray-900">
                {organizations.value.filter(org => org.status === 'active').length}
              </p>
            </div>
          </div>
        </div>
        
        <div class="card">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-primary-100 rounded-lg flex items-center justify-center">
                <span class="text-primary-600">🏗️</span>
              </div>
            </div>
            <div class="ml-3">
              <p class="text-sm font-medium text-gray-600">Prime Contractors</p>
              <p class="text-lg font-semibold text-gray-900">
                {organizations.value.filter(org => org.organization_type === 'prime_contractor').length}
              </p>
            </div>
          </div>
        </div>
        
        <div class="card">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-secondary-100 rounded-lg flex items-center justify-center">
                <span class="text-secondary-600">🤝</span>
              </div>
            </div>
            <div class="ml-3">
              <p class="text-sm font-medium text-gray-600">Subcontractors</p>
              <p class="text-lg font-semibold text-gray-900">
                {organizations.value.filter(org => org.organization_type === 'subcontractor').length}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Organizations List */}
      {loading.value ? (
        <div class="card">
          <div class="flex items-center justify-center py-12">
            <div class="loading-spinner w-8 h-8"></div>
            <span class="ml-3 text-gray-600">Loading organizations...</span>
          </div>
        </div>
      ) : (
        <OrganizationList organizations={organizations.value} />
      )}

      {/* Create Organization Modal */}
      {showCreateForm.value && (
        <div class="fixed inset-0 z-50 overflow-y-auto">
          <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
            
            <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
              <OrganizationForm
                onClose$={() => showCreateForm.value = false}
                onSuccess$={(newOrg) => {
                  organizations.value = [...organizations.value, newOrg];
                  showCreateForm.value = false;
                }}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
});

export const head: DocumentHead = {
  title: 'Organizations - Waste Management Intelligence System',
  meta: [
    {
      name: 'description',
      content: 'Manage contractors, subcontractors, and municipal organizations in the waste management system',
    },
  ],
};
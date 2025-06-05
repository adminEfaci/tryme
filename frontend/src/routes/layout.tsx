import { component$, Slot, useSignal } from '@builder.io/qwik';
import { routeLoader$ } from '@builder.io/qwik-city';
import { Sidebar } from '~/components/layout/sidebar';
import { Header } from '~/components/layout/header';

export const useServerTimeLoader = routeLoader$(() => {
  return {
    date: new Date().toISOString(),
  };
});

export default component$(() => {
  const sidebarOpen = useSignal(true);

  return (
    <div class="min-h-screen bg-gray-50">
      {/* Sidebar */}
      <Sidebar isOpen={sidebarOpen} />
      
      {/* Main Content */}
      <div class={`transition-all duration-300 ${sidebarOpen.value ? 'ml-64' : 'ml-0'}`}>
        {/* Header */}
        <Header onToggleSidebar$={() => sidebarOpen.value = !sidebarOpen.value} />
        
        {/* Page Content */}
        <main class="p-6">
          <Slot />
        </main>
      </div>
    </div>
  );
});
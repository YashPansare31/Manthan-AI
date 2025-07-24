import { Skeleton } from '@/components/ui/skeleton';

export const TranscriptionSkeleton = () => (
  <div className="glass rounded-xl p-6 space-y-4">
    <div className="flex items-center justify-between mb-4">
      <Skeleton className="h-6 w-32" />
      <Skeleton className="h-8 w-20" />
    </div>
    <div className="space-y-3">
      <Skeleton className="h-4 w-full" />
      <Skeleton className="h-4 w-5/6" />
      <Skeleton className="h-4 w-4/5" />
      <Skeleton className="h-4 w-full" />
      <Skeleton className="h-4 w-3/4" />
      <Skeleton className="h-4 w-5/6" />
      <Skeleton className="h-4 w-2/3" />
    </div>
  </div>
);

export const SummarySkeleton = () => (
  <div className="glass rounded-xl p-6 space-y-4">
    <div className="flex items-center justify-between mb-4">
      <Skeleton className="h-6 w-40" />
      <div className="flex space-x-2">
        <Skeleton className="h-8 w-16" />
        <Skeleton className="h-8 w-24" />
      </div>
    </div>
    <div className="space-y-3">
      <Skeleton className="h-4 w-full" />
      <Skeleton className="h-4 w-4/5" />
      <Skeleton className="h-4 w-full" />
      <Skeleton className="h-4 w-3/4" />
    </div>
  </div>
);

export const ActionItemsSkeleton = () => (
  <div className="glass rounded-xl p-6 space-y-4">
    <div className="flex items-center justify-between mb-4">
      <Skeleton className="h-6 w-28" />
      <Skeleton className="h-6 w-16" />
    </div>
    <div className="space-y-3">
      {[1, 2, 3, 4].map((i) => (
        <div key={i} className="flex items-center space-x-3 p-3 glass-strong rounded-lg">
          <Skeleton className="w-4 h-4 rounded" />
          <Skeleton className="h-4 flex-1" />
          <Skeleton className="w-6 h-6" />
        </div>
      ))}
    </div>
  </div>
);

export const ResultsSkeleton = () => (
  <div className="space-y-6 animate-fade-in">
    {/* Quick Stats Skeleton */}
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
      {[1, 2, 3, 4].map((i) => (
        <div key={i} className="glass rounded-xl p-4 text-center space-y-2">
          <Skeleton className="w-5 h-5 mx-auto" />
          <Skeleton className="h-3 w-20 mx-auto" />
          <Skeleton className="h-5 w-12 mx-auto" />
        </div>
      ))}
    </div>

    {/* Search Bar Skeleton */}
    <Skeleton className="h-10 w-full rounded-lg" />

    {/* Tabs Skeleton */}
    <div className="space-y-6">
      <div className="glass-strong rounded-lg p-1">
        <div className="grid grid-cols-4 gap-1">
          {[1, 2, 3, 4].map((i) => (
            <Skeleton key={i} className="h-10" />
          ))}
        </div>
      </div>
      
      <TranscriptionSkeleton />
    </div>
  </div>
);
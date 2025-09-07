import { useAuth0 } from '@auth0/auth0-react'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Button } from '@/components/ui/button'
import { LogOut } from 'lucide-react'

export const UserProfile = () => {
  const { user, isAuthenticated, logout } = useAuth0()

  if (!isAuthenticated || !user) return null

  const handleLogout = () => {
    logout({ logoutParams: { returnTo: window.location.origin } })
  }

  return (
    <div className="flex items-center gap-3">
      <Avatar>
        <AvatarImage src={user.picture} alt={user.name} />
        <AvatarFallback>
          {user.name?.charAt(0).toUpperCase() || 'U'}
        </AvatarFallback>
      </Avatar>
      <div className="flex flex-col">
        <span className="text-sm font-medium">{user.name}</span>
        <span className="text-xs text-muted-foreground">{user.email}</span>
      </div>
      <Button 
        onClick={handleLogout}
        variant="outline"
        size="sm"
        className="flex items-center gap-2"
      >
        <LogOut size={14} />
        Sign Out
      </Button>
    </div>
  )
}
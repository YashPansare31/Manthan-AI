import { useAuth0 } from '@auth0/auth0-react'
import { Button } from '@/components/ui/button'
import { LogOut } from 'lucide-react'

export const LogoutButton = () => {
  const { logout, isLoading } = useAuth0()

  return (
    <Button 
      onClick={() => logout({ logoutParams: { returnTo: window.location.origin } })}
      disabled={isLoading}
      variant="outline"
      className="flex items-center gap-2"
    >
      <LogOut size={16} />
      {isLoading ? 'Loading...' : 'Sign Out'}
    </Button>
  )
}
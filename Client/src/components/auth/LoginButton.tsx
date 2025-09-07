import { useAuth0 } from '@auth0/auth0-react'
import { Button } from '@/components/ui/button'
import { LogIn } from 'lucide-react'

export const LoginButton = () => {
  const { loginWithRedirect, isLoading } = useAuth0()

  return (
    <Button 
      onClick={() => loginWithRedirect()}
      disabled={isLoading}
      className="flex items-center gap-2"
    >
      <LogIn size={16} />
      {isLoading ? 'Loading...' : 'Sign In'}
    </Button>
  )
}
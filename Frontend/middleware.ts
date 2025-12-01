
import { withAuth } from "next-auth/middleware";

// Protect routes
export default withAuth({
  pages: {
    signIn: "/login", // redirect if unauthenticated
  },
});

// Define which paths are protected
export const config = {
  matcher: ["/chat/:path*"],
};

import NextAuth from "next-auth"
import Google from "next-auth/providers/google"

const handler = NextAuth({
  providers: [
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    })
  ],

  callbacks: {
  async jwt({ token, account }) {
    if (account) {
      token.idToken = account.id_token;   // save google id_token
    }
    return token;
  },

  async session({ session, token }) {
    session.idToken = token.idToken;      // make it available in frontend
    return session;
  },
}
})

export { handler as GET, handler as POST }

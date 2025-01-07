import { Session, User } from "next-auth"

declare module "next-auth" {

    interface Session {
        id: string;
        sessionToken: string;
        user: User;
        expires: Date;
    }

    interface User {
        id: string;
        email?: string | null;
        name?: string | null;
    }
}

declare module "next-auth/jwt" {
    interface JWT {
        access_token?: string;
        user?: User
    }
}
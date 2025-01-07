import { PrismaClient } from '@prisma/client'
import pkg from 'bcryptjs';
const { hash } = pkg;
const prisma = new PrismaClient()

async function main() {
    const hashedPassword = await hash('password123', 12)

    const user = await prisma.user.upsert({
        where: { email: 'test@example.com' },
        update: {},
        create: {
            email: 'test@example.com',
            name: 'Test User',
            password: hashedPassword,
        },
    })

    console.log({ user })
}

main()
    .catch((e) => {
        console.error(e)
        process.exit(1)
    })
    .finally(async () => {
        await prisma.$disconnect()
    })
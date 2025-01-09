/*
  Warnings:

  - You are about to drop the `Source` table. If the table is not empty, all the data it contains will be lost.

*/
-- CreateEnum
CREATE TYPE "SourceStatus" AS ENUM ('PENDING', 'COMPLETED', 'FAILED');

-- DropTable
DROP TABLE "Source";

-- CreateTable
CREATE TABLE "Document" (
    "id" STRING NOT NULL,
    "name" STRING NOT NULL,
    "content" STRING NOT NULL DEFAULT '',
    "status" "SourceStatus" NOT NULL DEFAULT 'PENDING',
    "userId" STRING NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Document_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "Document" ADD CONSTRAINT "Document_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

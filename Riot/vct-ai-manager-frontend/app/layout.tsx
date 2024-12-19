import type { Metadata } from 'next'
import { Roboto, Montserrat } from 'next/font/google'
import './globals.css'

const roboto = Roboto({ subsets: ['latin'], weight: ['400', '700'], variable: '--font-roboto' })
const montserrat = Montserrat({ subsets: ['latin'], weight: ['700'], variable: '--font-montserrat' })

export const metadata: Metadata = {
  title: 'VCT AI Manager',
  description: 'Esports Manager Challenge for VCT',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh">
      <body className={`${roboto.variable} ${montserrat.variable} font-roboto bg-light-gray`}>{children}</body>
    </html>
  )
}
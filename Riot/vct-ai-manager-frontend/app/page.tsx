import Logo from '@/components/Logo';
import ChatInterface from '@/components/ChatInterface';

export default function Home() {
    return (
        <main className="flex min-h-screen flex-col items-center justify-start p-6 sm:p-12 bg-gray-900">
            <Logo />
            <div className="w-full max-w-4xl mt-8">
                <h2 className="text-2xl font-montserrat font-bold text-teal mb-4">欢迎来到 VCT AI 管理器</h2>
                <p className="text-light-gray mb-6">开始与我们的AI助手聊天，探索电子竞技管理的世界！</p>
                <ChatInterface />
            </div>
        </main>
    );
}
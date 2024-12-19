import { NextResponse } from 'next/server';

export async function POST(request: Request) {
    const { message } = await request.json();

    // 这里是模拟的AI响应，实际项目中应该连接到真实的AI服务
    const aiResponse = `这是对 "${message}" 的模拟AI响应。`;

    return NextResponse.json({ message: aiResponse });
}
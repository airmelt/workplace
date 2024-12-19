export default function Logo() {
    return (
        <h1 className="text-4xl font-montserrat font-bold text-white">
            VCT{' '}
            <span className="relative">
                <span className="text-teal">AI</span>
                <span className="absolute -top-1 -right-3 text-coral text-3xl transform rotate-12">⚡</span>
            </span>{' '}
            Manager
        </h1>
    );
}
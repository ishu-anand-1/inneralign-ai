const Header = () => {
  return (
    <header className="w-full bg-white border-b border-gray-200">
      <div className="max-w-md mx-auto px-4 py-4 text-center">
        {/* App Title */}
        <h1 className="text-2xl font-semibold tracking-tight text-indigo-600">
          InnerAlign AI
        </h1>

        {/* Subtitle */}
        <p className="mt-1 text-sm text-gray-500">
          Advanced Handwriting Analysis Engine
        </p>
      </div>
    </header>
  );
};

export default Header;

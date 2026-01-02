import Link from "next/link";

export default function HomePage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-4 text-center">
      <h1 className="text-4xl font-extrabold text-indigo-600 mb-4">
        Evolution of Todo
      </h1>
      <p className="text-xl text-gray-600 mb-8 max-w-md">
        A secure,   multi-user task management application built with FastAPI and Next.js.
      </p>
      <div className="flex space-x-4">
        <Link
          href="/login"
          className="bg-indigo-600 text-white px-6 py-3 rounded-md font-medium hover:bg-indigo-700 transition"
        >
          Login
        </Link>
        <Link
          href="/register"
          className="bg-white text-indigo-600 border border-indigo-600 px-6 py-3 rounded-md font-medium hover:bg-indigo-50 transition"
        >
          Register
        </Link>
      </div>
    </div>
  );
}

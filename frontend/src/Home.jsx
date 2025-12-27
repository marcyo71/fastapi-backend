import React from "react";
import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Benvenuto 🚀</h1>
      <Link
        to="/dashboard"
        className="inline-block mr-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Vai alla Dashboard
      </Link>
      <Link
        to="/checkout"
        className="inline-block px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
      >
        Vai al Checkout
      </Link>
    </div>
  );
}

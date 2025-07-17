'use client';

import { SignUp } from '@clerk/nextjs';

export default function Page() {
  return (
    <div className="place-items-center">
      <SignUp routing="path" signInUrl="/login" />
    </div>
  );
}
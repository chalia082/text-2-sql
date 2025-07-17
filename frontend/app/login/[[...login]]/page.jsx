'use client';

import { SignIn } from '@clerk/nextjs';
import React from 'react';

export default function Page() {
  return (
    <div className="place-items-center">
      <SignIn routing="path" signUpUrl="/signup" />
    </div>
  );
}
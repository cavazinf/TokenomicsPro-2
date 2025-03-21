import React from 'react';
import { Link } from 'wouter';
import { Button } from '@/components/ui/button';

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4 text-center">
      <h1 className="text-6xl font-bold text-gray-200">404</h1>
      <h2 className="mt-4 text-2xl font-semibold">Página não encontrada</h2>
      <p className="mt-4 text-muted-foreground max-w-md">
        A página que você está procurando não existe ou foi movida.
      </p>
      <Link href="/">
        <Button className="mt-8">
          Voltar para a Dashboard
        </Button>
      </Link>
    </div>
  );
}
import Link from 'next/link';
import React from 'react';

const AboutPage = () => (
    <main style={{ padding: '2rem' }}>
        <h1>About:</h1>
        <br />
        <p>
            This app is for educational purpose, demonstrating how to build a web
            application on Next.js framework. It showcases features such as routing, dynamic
            pages, data fetching, mix of SSR (Server Side Rendering) and CSR (Client Side Rendering),
            Server Components for data dislay and Server Actions for submitting forms.
        </p>
        <br />
        <p>
            <Link href="https://github.com/peanut101codes/my-dev-work/tree/main/earthquakes-app" 
                target="_blank" rel="noopener noreferrer"
                className="text-blue-600 hover:underline">
                Source Code on GitHub
            </Link>
        </p>
    </main>
);

export default AboutPage;
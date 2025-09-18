/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      { source: "/",          destination: "/index.html" },
      { source: "/builder",   destination: "/builder.html" },
      { source: "/review",    destination: "/review.html" },
      { source: "/trainings", destination: "/trainings.html" },
    ];
  },
  eslint: { ignoreDuringBuilds: true },
  typescript: { ignoreBuildErrors: true },
};
module.exports = nextConfig;

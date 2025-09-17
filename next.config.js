/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      { source: "/builder",   destination: "/cs50/builder.html" },
      { source: "/review",    destination: "/cs50/review.html" },
      { source: "/trainings", destination: "/cs50/trainings.html" }
    ];
  }
};
module.exports = nextConfig;

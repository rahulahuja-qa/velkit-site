export async function getServerSideProps() {
  return { redirect: { destination: "/review.html", permanent: false } };
}
export default function Review() { return null; }

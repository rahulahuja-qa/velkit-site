export async function getServerSideProps() {
  return { redirect: { destination: "/builder.html", permanent: false } };
}
export default function Builder() { return null; }

export async function getServerSideProps() {
  return { redirect: { destination: "/trainings.html", permanent: false } };
}
export default function Trainings() { return null; }

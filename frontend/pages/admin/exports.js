import Layout from "../../components/Layout";
export default function ExportsPage() {
  return (
    <Layout>
      <div className="card">
        <h1>Dışa Aktar</h1>
        <div className="nav">
          <a href="/api/exports/units.xlsx"><button>Excel İndir</button></a>
          <a href="/api/exports/units.pdf"><button>PDF İndir</button></a>
        </div>
      </div>
    </Layout>
  )
}

import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import { api, getUser } from "../lib/api";

export default function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [expenses, setExpenses] = useState([]);
  const [payments, setPayments] = useState([]);
  const user = typeof window !== "undefined" ? getUser() : null;

  useEffect(() => {
    api("/dashboard").then(setSummary).catch(console.error);
    api("/payments").then(setPayments).catch(console.error);
    if (!user?.is_admin) api("/dashboard/my-expenses").then(setExpenses).catch(console.error);
  }, []);

  return (
    <Layout>
      <div className="card"><h1>{user?.is_admin ? "Yönetici Paneli" : "Borç Özeti"}</h1></div>
      {summary && user?.is_admin && <div className="grid">
        <div className="card"><h3>Toplam Gider</h3><p>{summary.total_expenses} TL</p></div>
        <div className="card"><h3>Toplam Tahsilat</h3><p>{summary.total_collected} TL</p></div>
        <div className="card"><h3>Kalan</h3><p>{summary.total_outstanding} TL</p></div>
        <div className="card"><h3>Daire Sayısı</h3><p>{summary.unit_count}</p></div>
      </div>}
      {summary && !user?.is_admin && <div className="grid">
        <div className="card"><h3>Toplam Borç</h3><p>{summary.total_debt} TL</p></div>
        <div className="card"><h3>Toplam Ödenen</h3><p>{summary.total_paid} TL</p></div>
        <div className="card"><h3>Kalan</h3><p>{summary.balance} TL</p></div>
      </div>}
      {!user?.is_admin && <div className="card">
        <h2>Giderlerim</h2>
        <table><thead><tr><th>Başlık</th><th>Kategori</th><th>Vade</th><th>Tutar</th></tr></thead><tbody>
          {expenses.map(item => <tr key={item.id}><td>{item.title}</td><td>{item.category}</td><td>{new Date(item.due_date).toLocaleDateString("tr-TR")}</td><td>{item.amount} TL</td></tr>)}
        </tbody></table>
      </div>}
      <div className="card">
        <h2>Ödemeler</h2>
        <table><thead><tr><th>Daire ID</th><th>Tutar</th><th>Açıklama</th><th>Tarih</th></tr></thead><tbody>
          {payments.map(item => <tr key={item.id}><td>{item.unit_id}</td><td>{item.amount} TL</td><td>{item.description}</td><td>{new Date(item.paid_at).toLocaleDateString("tr-TR")}</td></tr>)}
        </tbody></table>
      </div>
    </Layout>
  )
}

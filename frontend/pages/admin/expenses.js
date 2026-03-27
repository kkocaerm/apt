import { useEffect, useState } from "react";
import Layout from "../../components/Layout";
import { api } from "../../lib/api";

export default function ExpensesPage() {
  const [items, setItems] = useState([]);
  const [form, setForm] = useState({ title:"", category:"aidat", total_amount:"", due_date:"", notes:"" });
  const [message, setMessage] = useState("");

  function load(){ api("/expenses").then(setItems).catch(console.error); }
  useEffect(()=>{ load(); },[]);

  async function submit(e){
    e.preventDefault();
    await api("/expenses", { method:"POST", body:JSON.stringify({ ...form, total_amount:Number(form.total_amount), due_date:new Date(form.due_date).toISOString() }) });
    setForm({ title:"", category:"aidat", total_amount:"", due_date:"", notes:"" });
    setMessage("Gider eklendi ve dairelere dağıtıldı");
    load();
  }

  return (
    <Layout>
      <div className="card">
        <h1>Giderler</h1>
        <form onSubmit={submit}>
          <div className="row">
            <input placeholder="Başlık" value={form.title} onChange={e=>setForm({...form, title:e.target.value})} />
            <select value={form.category} onChange={e=>setForm({...form, category:e.target.value})}>
              <option value="aidat">Aidat</option>
              <option value="elektrik">Elektrik</option>
              <option value="doğalgaz">Doğalgaz</option>
              <option value="su">Su</option>
              <option value="diğer">Diğer</option>
            </select>
          </div>
          <div style={{height:12}} />
          <div className="row">
            <input type="number" step="0.01" placeholder="Toplam tutar" value={form.total_amount} onChange={e=>setForm({...form, total_amount:e.target.value})} />
            <input type="date" value={form.due_date} onChange={e=>setForm({...form, due_date:e.target.value})} />
          </div>
          <div style={{height:12}} />
          <textarea placeholder="Notlar" value={form.notes} onChange={e=>setForm({...form, notes:e.target.value})} />
          <div style={{height:12}} />
          <button type="submit">Gider Oluştur</button>
        </form>
        {message && <p className="success">{message}</p>}
      </div>
      <div className="card">
        <table><thead><tr><th>Başlık</th><th>Kategori</th><th>Tutar</th><th>Vade</th></tr></thead><tbody>
          {items.map(item => <tr key={item.id}><td>{item.title}</td><td>{item.category}</td><td>{item.total_amount} TL</td><td>{new Date(item.due_date).toLocaleDateString("tr-TR")}</td></tr>)}
        </tbody></table>
      </div>
    </Layout>
  )
}

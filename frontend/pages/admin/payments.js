import { useEffect, useState } from "react";
import Layout from "../../components/Layout";
import { api } from "../../lib/api";

export default function PaymentsPage() {
  const [payments, setPayments] = useState([]);
  const [units, setUnits] = useState([]);
  const [form, setForm] = useState({ unit_id:"", amount:"", description:"", paid_at:"" });

  function load(){ api("/payments").then(setPayments).catch(console.error); api("/units").then(setUnits).catch(console.error); }
  useEffect(()=>{ load(); },[]);

  async function submit(e){
    e.preventDefault();
    await api("/payments", { method:"POST", body:JSON.stringify({ unit_id:Number(form.unit_id), amount:Number(form.amount), description:form.description, paid_at:new Date(form.paid_at).toISOString() }) });
    setForm({ unit_id:"", amount:"", description:"", paid_at:"" });
    load();
  }

  return (
    <Layout>
      <div className="card">
        <h1>Ödeme Girişi</h1>
        <form onSubmit={submit}>
          <div className="row">
            <select value={form.unit_id} onChange={e=>setForm({...form, unit_id:e.target.value})}>
              <option value="">Daire seç</option>
              {units.map(u => <option key={u.unit_id} value={u.unit_id}>{u.unit_name}</option>)}
            </select>
            <input type="number" step="0.01" placeholder="Tutar" value={form.amount} onChange={e=>setForm({...form, amount:e.target.value})} />
          </div>
          <div style={{height:12}} />
          <div className="row">
            <input placeholder="Açıklama" value={form.description} onChange={e=>setForm({...form, description:e.target.value})} />
            <input type="date" value={form.paid_at} onChange={e=>setForm({...form, paid_at:e.target.value})} />
          </div>
          <div style={{height:12}} />
          <button type="submit">Ödeme Kaydet</button>
        </form>
      </div>
      <div className="card">
        <table><thead><tr><th>Daire</th><th>Tutar</th><th>Açıklama</th><th>Tarih</th></tr></thead><tbody>
          {payments.map(item => <tr key={item.id}><td>{item.unit_id}</td><td>{item.amount} TL</td><td>{item.description}</td><td>{new Date(item.paid_at).toLocaleDateString("tr-TR")}</td></tr>)}
        </tbody></table>
      </div>
    </Layout>
  )
}

import { useEffect, useState } from "react";
import Layout from "../../components/Layout";
import { api } from "../../lib/api";

export default function InvitesPage() {
  const [units, setUnits] = useState([]);
  const [form, setForm] = useState({ unit_id:"", email:"" });
  const [result, setResult] = useState(null);

  useEffect(()=>{ api("/units").then(setUnits).catch(console.error); },[]);

  async function submit(e){
    e.preventDefault();
    const data = await api("/units/invite", { method:"POST", body:JSON.stringify({ unit_id:Number(form.unit_id), email:form.email }) });
    setResult(data);
  }

  return (
    <Layout>
      <div className="card">
        <h1>Davet Gönder</h1>
        <form onSubmit={submit}>
          <div className="row">
            <select value={form.unit_id} onChange={e=>setForm({...form, unit_id:e.target.value})}>
              <option value="">Daire seç</option>
              {units.map(u => <option key={u.unit_id} value={u.unit_id}>{u.unit_name}</option>)}
            </select>
            <input placeholder="E-posta" value={form.email} onChange={e=>setForm({...form, email:e.target.value})} />
          </div>
          <div style={{height:12}} />
          <button type="submit">Davet Oluştur</button>
        </form>
      </div>
      {result && <div className="card"><p className="success">{result.message}</p><p>Davet linki: {result.link}</p><p className="small">SMTP yoksa bu linki manuel paylaş.</p></div>}
    </Layout>
  )
}

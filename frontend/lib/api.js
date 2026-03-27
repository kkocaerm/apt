const API_BASE = process.env.NEXT_PUBLIC_API_URL || "/api";
export function getToken(){ if(typeof window==="undefined") return null; return localStorage.getItem("token"); }
export function getUser(){ if(typeof window==="undefined") return null; const raw=localStorage.getItem("user"); return raw?JSON.parse(raw):null; }
export function setAuth(data){ localStorage.setItem("token",data.access_token); localStorage.setItem("user",JSON.stringify(data.user)); }
export function clearAuth(){ localStorage.removeItem("token"); localStorage.removeItem("user"); }
export async function api(path, options={}) {
  const token=getToken();
  const headers={"Content-Type":"application/json", ...(options.headers||{})};
  if(token) headers.Authorization=`Bearer ${token}`;
  const res=await fetch(`${API_BASE}${path}`, {...options, headers});
  const ct=res.headers.get("content-type")||"";
  const data=ct.includes("application/json")?await res.json():await res.text();
  if(!res.ok) throw new Error(data.detail || data || "Request failed");
  return data;
}

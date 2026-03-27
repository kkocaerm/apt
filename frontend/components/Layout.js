import Link from "next/link";
import { useRouter } from "next/router";
import { clearAuth, getUser } from "../lib/api";

export default function Layout({ children }) {
  const router = useRouter();
  const user = typeof window !== "undefined" ? getUser() : null;
  function logout(){ clearAuth(); router.push("/login"); }
  return (
    <div className="container">
      <div className="nav">
        <Link href="/dashboard">Dashboard</Link>
        {user?.is_admin && <Link href="/admin/units">Daireler</Link>}
        {user?.is_admin && <Link href="/admin/expenses">Giderler</Link>}
        {user?.is_admin && <Link href="/admin/payments">Ödemeler</Link>}
        {user?.is_admin && <Link href="/admin/invites">Davetler</Link>}
        {user?.is_admin && <Link href="/admin/exports">Dışa Aktar</Link>}
        <button style={{width:"auto"}} onClick={logout}>Çıkış</button>
      </div>
      {children}
    </div>
  )
}

const LINKS = {
  mensual: "https://mpago.la/2LprVEr", // $49/mes
  anual: "https://mpago.la/28kWMCz"   // $249/año
};

export default function Paywall({ onClose }: { onClose: () => void }) {
  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl p-6 max-w-sm w-full text-center">
        <h2 className="text-xl font-bold">🚀 Te acabaste los 2 créditos gratis</h2>
        <p className="text-sm text-gray-600 mt-2">Pasa a PRO para conversiones ilimitadas</p>
        
        <div className="mt-5 space-y-3">
          <a href={LINKS.mensual} target="_blank" className="block w-full bg-blue-600 text-white py-3 rounded-xl font-bold">
            PRO MES - $49/mes
          </a>
          <a href={LINKS.anual} target="_blank" className="block w-full bg-green-600 text-white py-3 rounded-xl font-bold">
            PRO AÑO - $249/año (Ahorra $339)
          </a>
        </div>

        <p className="text-xs text-gray-500 mt-4">Después de pagar, mándame comprobante por WhatsApp y te activo PRO al instante.</p>
        <button onClick={onClose} className="text-xs text-gray-400 mt-3">Cerrar</button>
      </div>
    </div>
  )
}

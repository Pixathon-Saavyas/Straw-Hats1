import Image from "next/image"

function PaymentPage() {
  return (
    <section className="w-screen h-screen grid grid-cols-12">
      <section className="col-span-8 h-screen overflow-auto p-10">
        <p className="text-white text-5xl font-bold">Mars Trip Plan</p>
        <div className="flex items-center justify-center w-full h-64 overflow-hidden rounded-2xl mt-5">
          <Image 
            src="/mars.jpg"
            height={200}
            width={1000}
            alt=""
          />
        </div>
        <div>
          <p className="text-3xl font-semibold mt-5">Details</p>
          <p className="text-2xl mt-2">Rocket: Falcon 1</p>
          <p className="text-2xl">Launchpad: South California</p>
          <p className="text-2xl">Date: <code>2024-02-01</code></p>
          <p className="text-sm absolute bottom-10 left-10">Session Id: 1212122212</p>
        </div>
      </section>
      <section className="col-span-4 sticky top-0 p-10">
        <div className=" bg-zinc-900 p-10">
          <p className="text-center font-semibold text-yellow-400 text-2xl">TheMartian.</p>
          <p className="text-center text-5xl mt-5"><code>Rs.1cr</code></p>
          <div className="px-5">
            <p className="text-sm text-gray-400 mt-8">+ Food facilities (3 meals/24 Earth hours)</p>
            <p className="text-sm text-gray-400 mt-2">+ Interflight Shopping facilities</p>
          </div>
          <button className="bg-black p-8 py-5 mt-10 w-full">Proceed for Payment</button>
        </div>
      </section>
    </section>
  )
}

export default PaymentPage
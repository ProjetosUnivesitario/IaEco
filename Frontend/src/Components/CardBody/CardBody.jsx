const CardBody = ({ icon: Icon, title, value, unit, bgColor, textColor, progress, description, subdescription, items, pendingItem }) => (
    <div className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden">
      <div className={`${bgColor} p-6 text-white relative`}>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <div className="bg-white/20 p-3 rounded-xl">
              <Icon size={24} />
            </div>
            <div>
              <h3 className="text-lg font-semibold">{title}</h3>
              <p className="text-white/80 text-sm">{description}</p>
            </div>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold">{value}</div>
            <div className="text-white/80 text-sm">{unit}</div>
          </div>
        </div>
        
        <div className="bg-white/20 rounded-full h-2 mb-2">
          <div 
            className="bg-white rounded-full h-2 transition-all duration-500"
            style={{ width: `${progress}%` }}
          ></div>
        </div>
        <div className="text-white/80 text-xs">{progress}% concluído</div>
      </div>
      
      <div className="p-6">
        <p className="text-gray-600 text-sm mb-4">{subdescription}</p>
        <div className="space-y-2">
          {items.map((item, index) => (
            <div key={index} className="flex items-center text-sm">
              <div className="w-2 h-2 bg-green-400 rounded-full mr-3"></div>
              <span className="text-gray-700">{item}</span>
            </div>
          ))}
          {pendingItem && (
            <div className="flex items-center text-sm">
              <div className="w-2 h-2 bg-orange-400 rounded-full mr-3"></div>
              <span className="text-orange-600">{pendingItem} (Pendente)</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );

export default CardBody;
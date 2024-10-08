import { createContext, useContext, useState, useEffect } from "react";

interface MicAccessContextType {
	hasMicAccess: boolean;
}

const MicAccessContext = createContext<MicAccessContextType | undefined>(undefined)

function useMicAccess(): MicAccessContextType {
	const context = useContext(MicAccessContext)
	if (context === undefined) {
		throw new Error("useMicAccess must be used within a MicAccessProvider")
	}
	return context
}

interface MicAccessProviderProps { children: React.ReactNode }
function MicAccessProvider({ children }: MicAccessProviderProps) {
	const [hasMicAccess, setHasMicAccess] = useState<boolean>(false)

	useEffect(() => {
		const checkMicAccess = async () => {
			try {
				await navigator.mediaDevices.getUserMedia({ audio: true });
				setHasMicAccess(true);
			} catch (error) {
				setHasMicAccess(false);
			}
		};

		checkMicAccess();
	}, []);

	return (
		<MicAccessContext.Provider value={{ hasMicAccess }}>
			{children}
		</MicAccessContext.Provider>
	);
}

export { useMicAccess, MicAccessProvider }
export default MicAccessContext
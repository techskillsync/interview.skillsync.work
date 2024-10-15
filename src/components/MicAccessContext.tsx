import { createContext, useContext, useState, useEffect } from "react";

interface MicAccessContextType {
	has_mic_access: boolean;
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
	const [has_mic_access, set_has_mic_access] = useState<boolean>(false)

	useEffect(() => {
		const checkMicAccess = async () => {
			try {
				await navigator.mediaDevices.getUserMedia({ audio: true });
				set_has_mic_access(true);
			} catch (error) {
				set_has_mic_access(false);
			}
		};

		checkMicAccess();
	}, []);

	return (
		<MicAccessContext.Provider value={{ has_mic_access }}>
			{children}
		</MicAccessContext.Provider>
	);
}

export { useMicAccess, MicAccessProvider }
export default MicAccessContext
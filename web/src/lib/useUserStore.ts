import { create } from 'zustand';

// UserInfo 类型为 dict
interface UserStore {
  userInfo: Record<string, any> | null;
  personId: string | null;
  isLoggedIn: boolean;
  setUserInfo: (userInfo: Record<string, any> | null) => void;
  setPersonId: (personId: string | null) => void;
  setIsLoggedIn: (isLoggedIn: boolean) => void;
  clear: () => void;
  init: (data: { userInfo: Record<string, any>; personId: string; isLoggedIn: boolean }) => void;
}

export const useUserStore = create<UserStore>()((set) => ({
  userInfo: null,
  personId: null,
  isLoggedIn: false,
  setUserInfo: (userInfo) => set({ userInfo }),
  setPersonId: (personId) => set({ personId }),
  setIsLoggedIn: (isLoggedIn) => set({ isLoggedIn }),
  clear: () => set({ userInfo: null, personId: null, isLoggedIn: false }),
  init: (data) => set({
    userInfo: data.userInfo,
    personId: data.personId,
    isLoggedIn: data.isLoggedIn,
  }),
})); 
'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { useToast } from '@/components/ui/use-toast';
import ProfileForm from '@/components/profile/profile-form';
import TableManager from '@/components/tables/table-manager';
import { userStore } from '@/lib/store';

export default function ProfilePage() {
  const [activeTab, setActiveTab] = useState('profile');
  const [profileData, setProfileData] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { toast } = useToast();
  const router = useRouter();

  useEffect(() => {
    const fetchProfileData = async () => {
      try {
        setIsLoading(true);
        
        // 检查登录状态
        const loginStatus = userStore.get('isLoggedIn');
        console.log('当前登录状态:', loginStatus);
        if (!loginStatus) {
          toast({
            title: '未登录',
            description: '请先登录后再访问个人资料页面',
            variant: 'destructive',
          });
          router.push('/login');
          return;
        }
        
        // 然后尝试从userStore(store.ts)获取
        const storedUserInfo = userStore.get('userInfo');
        if (storedUserInfo) {
          console.log('从localStorage加载用户信息');
          setProfileData(storedUserInfo);
          return;
        }
        
        // 最后加载模板数据
        console.log('加载模板数据');
        const response = await fetch('/form-template.json');
        if (response.ok) {
          const templateData = await response.json();
          setProfileData(templateData);
        } else {
          throw new Error('无法加载模板数据');
        }
      } catch (err) {
        console.error('加载个人资料失败:', err);
        setError('无法加载个人资料数据，请刷新页面重试');
        
        toast({
          title: '加载失败',
          description: '无法加载个人资料数据',
          variant: 'destructive',
        });
      } finally {
        setIsLoading(false);
      }
    };

    fetchProfileData();
  }, [router, toast]);




  // 渲染加载状态
  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="flex flex-col items-center space-y-4">
          <div className="w-16 h-16 border-4 border-t-blue-500 border-b-blue-700 border-l-blue-500 border-r-blue-700 rounded-full animate-spin"></div>
          <p className="text-lg font-medium">加载中...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="p-6 max-w-md mx-auto bg-white rounded-xl shadow-md flex flex-col items-center space-y-4">
          <div className="w-16 h-16 flex items-center justify-center rounded-full bg-red-100 text-red-500">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-10 h-10">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <p className="text-xl font-medium text-center">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors"
          >
            刷新页面
          </button>
        </div>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: -20 }}
      transition={{ duration: 0.5 }}
      className="container mx-auto py-6 px-4 sm:px-6"
    >

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-2 mb-8">
          <TabsTrigger value="profile" className="text-lg py-3">
            个人资料
          </TabsTrigger>
          <TabsTrigger value="tables" className="text-lg py-3">
            表格管理
          </TabsTrigger>
        </TabsList>
        
        <TabsContent value="profile" className="space-y-6">
          {profileData && (
            <ProfileForm 
              initialData={profileData} 
            />
          )}
        </TabsContent>
        
        <TabsContent value="tables" className="space-y-6">
          <TableManager />
        </TabsContent>
      </Tabs>
    </motion.div>
  );
}
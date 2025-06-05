'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import { useToast } from '@/components/ui/use-toast';
import { apiClient, userStore } from '@/lib/store';

export default function ProfileLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const { toast } = useToast();
  const [username, setUsername] = useState('');
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
    // 检查登录状态
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    const storedUsername = localStorage.getItem('username');
    
    if (!isLoggedIn) {
      toast({
        variant: 'destructive',
        title: '未登录',
        description: '请先登录系统',
      });
      router.push('/login');
    } else if (storedUsername) {
      setUsername(storedUsername);
    }
  }, [router, toast]);

  const handleLogout = () => {
    userStore.clearUserInfo();

    toast({
      title: '已退出登录',
      description: '您已成功退出系统',
    });
    router.push('/login');
  };

  if (!isClient) {
    return null; // 避免服务端渲染时尝试访问localStorage
  }

  return (
    <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
      {/* 顶部导航栏 */}
      <header className="sticky top-0 z-10 bg-white dark:bg-gray-800 shadow-sm">
        <div className="container mx-auto px-4 py-3 flex justify-between items-center">
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
            className="flex items-center space-x-2"
          >
            <span className="text-xl font-bold text-primary">"AI+” 档案管理</span>
          </motion.div>
          
          <motion.div 
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
            className="flex items-center space-x-4"
          >
            <div className="flex items-center space-x-2">
              <Avatar>
                <AvatarImage src="https://placekitten.com/100/100" alt={username} />
                <AvatarFallback>{username.slice(0, 2).toUpperCase()}</AvatarFallback>
              </Avatar>
              <span className="font-medium">{username}</span>
            </div>
            <Button variant="outline" size="sm" onClick={handleLogout}>
              退出登录
            </Button>
          </motion.div>
        </div>
      </header>

      {/* 主内容区 */}
      <main className="flex-1 container mx-auto px-4 py-6">
        {children}
      </main>

      {/* 页脚 */}
      <footer className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 py-4">
        <div className="container mx-auto px-4 text-center text-sm text-gray-500 dark:text-gray-400">
          © {new Date().getFullYear()} "AI+” 档案管理 - 保留所有权利
        </div>
      </footer>
    </div>
  );
}
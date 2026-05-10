'use client';

import { CalendarRange, Globe, LayoutDashboard, Shield, TrendingUp } from 'lucide-react';
import Link from 'next/link';
import { usePathname, useSearchParams } from 'next/navigation';
import {
	SidebarGroup,
	SidebarGroupLabel,
	SidebarMenu,
	SidebarMenuButton,
	SidebarMenuItem,
	useSidebar,
} from '@/components/ui/sidebar';

const items = [
	{ title: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
	{ title: 'Upcoming Fights', href: '/upcoming', icon: CalendarRange },
	{ title: 'Predictions', href: '/predictions', icon: TrendingUp },
	{ title: 'Browser', href: '/browser', icon: Globe },
];

const adminItems = [
	{
		title: 'Predictor Admin',
		href: '/admin/predict-train?admin=1',
		path: '/admin/predict-train',
		icon: Shield,
	},
];

export function NavMain() {
	const pathname = usePathname();
	const searchParams = useSearchParams();
	const { setOpenMobile } = useSidebar();
	const visibleItems = searchParams.get('admin') === '1' ? [...items, ...adminItems] : items;

	return (
		<SidebarGroup>
			<SidebarGroupLabel>Navigation</SidebarGroupLabel>
			<SidebarMenu>
				{visibleItems.map((item) => (
					<SidebarMenuItem key={item.href}>
						<SidebarMenuButton
							asChild
							isActive={pathname === ('path' in item ? item.path : item.href)}
							onClick={() => setOpenMobile(false)}
						>
							<Link href={item.href}>
								<item.icon />
								<span>{item.title}</span>
							</Link>
						</SidebarMenuButton>
					</SidebarMenuItem>
				))}
			</SidebarMenu>
		</SidebarGroup>
	);
}

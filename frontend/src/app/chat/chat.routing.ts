import { NgModule } from '@angular/core'
import { RouterModule, Routes } from '@angular/router'
import { NewsListComponent } from '@/news/containers/news-list/news-list.component'
import { NewsListItemComponent } from '@/news/components/news-list-item/news-list-item.component'
import { ChatListComponent } from '@/chat/containers/chat-list/chat-list.component'
import { ChatConversationComponent } from '@/chat/components/chat-conversation/chat-conversation.component'
import { ChatListItemComponent } from '@/chat/components/chat-list-item/chat-list-item.component'


export const COMPONENTS = [
    ChatListComponent,
    ChatListItemComponent,
    ChatConversationComponent
]

const routes: Routes =
    [
        {
            path: 'chat', component: ChatListComponent
        }
    ]


@NgModule( {
    imports: [ RouterModule.forChild( routes ) ],
    exports: [ RouterModule ]
} )
export class ChatRoutingModule {}
import { NgModule } from '@angular/core'
import { ChatRoutingModule, COMPONENTS } from '@/chat/chat.routing'
import { SharedModule } from '@/shared/shared.module'


@NgModule( {
    declarations: COMPONENTS,
    imports: [
        SharedModule,
        ChatRoutingModule
    ]
} )
export class ChatModule {}

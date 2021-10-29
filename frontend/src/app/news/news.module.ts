import { NgModule } from '@angular/core'
import { SharedModule } from '@/shared/shared.module'
import { COMPONENTS, NewsRoutingModule } from '@/news/news.routing'


@NgModule( {
    declarations: COMPONENTS,
    imports: [
        SharedModule,
        NewsRoutingModule
    ]
} )
export class NewsModule {}

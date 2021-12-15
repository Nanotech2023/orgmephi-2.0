import { NgModule } from '@angular/core'
import { HeaderComponent } from '@/layout/header/header.component'
import { FooterComponent } from '@/layout/footer/footer.component'
import { SharedModule } from '@/shared/shared.module'
import { HeaderConfirmAccountComponent } from '@/layout/header-confirm-account/header-confirm-account.component'
import { HeaderMenuComponent } from '@/layout/header-menu/header-menu.component'


const COMPONENTS = [
    HeaderComponent,
    FooterComponent,
    HeaderConfirmAccountComponent,
    HeaderMenuComponent
]


@NgModule( {
    declarations: COMPONENTS,
    exports: COMPONENTS,
    imports: [
        SharedModule
    ]
} )
export class LayoutModule {}